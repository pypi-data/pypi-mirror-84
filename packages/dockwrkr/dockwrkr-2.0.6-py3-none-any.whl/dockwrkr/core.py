import os
import sys
import logging
import re
from dockwrkr.monads import *
from dockwrkr.logs import *
from dockwrkr.exceptions import *
from dockwrkr.shell import Shell
from dockwrkr.utils import (readYAML, mergeDict, ensureList,
                            dateToAgo, walkUpForFile, writeToFile, expandLocalPath)
import dockwrkr.docker as docker

logger = logging.getLogger(__name__)


class Core(object):

    def __init__(self):
        self.options = {}
        self.configFile = None
        self.initialized = False
        self.config = {}
        return

    def initialize(self):
        if self.initialized:
            return OK(None)
        return self.loadConfig().then(defer(self.setInitialized, b=True))

    def setInitialized(self, b):
        self.initialized = b

    def loadConfig(self):
        return self.readConfigFile() >> self.setConfig

    def findConfigFile(self):
        if self.configFile:
            return OK(self.configFile)

        configFile = walkUpForFile(os.getcwd(), "dockwrkr.yml")
        if not configFile:
            return Fail(ConfigFileNotFound("Could not locate config file: dockwrkr.yml"))
        self.configFile = configFile
        return OK(configFile)

    def readConfigFile(self):
        return self.findConfigFile().bind(lambda f: Try.attempt(readYAML, f))

    def setConfig(self, config):
        mergeDict(self.config, config)
        return OK(self)

    def getRegistries(self):
        regs = self.config.get('registries', {})
        return regs

    def getNetworks(self):
        networks = self.config.get('networks', {})
        return networks

    def getDefinedServices(self, func=None, all=False):
        config_name = 'services'
        if not self.config.get(config_name):
            config_name = 'containers'
        return self.getDefinedContainers(config_name, func, all)

    def getDefinedJobs(self):
        return self.getDefinedContainers('jobs')

    def getDefinedContainers(self, configName='containers', func=None, all=False):
        graph = []
        containers = self.config.get(configName, {})

        for (container, container_config) in containers.items():
            if func == self.__start and all and not container_config.get('autostart', True):
                continue

            node = self.getContainerDependencies(container)
            graph.append(node)

        def resolveDependencies(node, resolved):
            for dep in node['deps']:
                depnode = self.getContainerDependencies(dep)
                if depnode['name'] not in resolved:
                    resolveDependencies(depnode, resolved)
            if node['name'] not in resolved:
                resolved.append(node['name'])
        resolved = []
        for node in graph:
            resolveDependencies(node, resolved)

        return resolved

    def getContainerDependencies(self, container):
        node = {}
        node['name'] = container
        deps = []
        config = self.getContainerConfig(container)
        if not config:
            raise InvalidContainerError("Container named '%s' is listed as a dependency but it is never defined." % container)
        if "link" in config:
            for link in ensureList(config['link']):
                deps.append(link.partition(':')[0])
        node['deps'] = deps
        return node

    def getBasePath(self):
        return os.path.dirname(self.configFile)

    def getContainerConfig(self, container):
        config = self.getServiceConfig(container)
        if config:
            return config
        return self.getJobConfig(container)

    def getServiceConfig(self, container):
        return self.config.get('services', self.config.get('containers', {})).get(container)

    def getJobConfig(self, container):
        return self.config.get('jobs', {}).get(container)

    def getContainerImage(self, container):
        conf = self.getContainerConfig(container)
        return conf.get('image', None)

    # Commands

    def readOrderedContainers(self, containers=[]):
        try:
            defined = self.getDefinedServices()
        except Exception as e:
            return Fail(e)
        missing = [x for x in containers if x not in defined]
        ordered = [x for x in defined if x in containers]
        if missing:
            return Fail(InvalidContainerError("Container '%s' not defined." % ' '.join(missing)))
        return OK(ordered)

    def create(self, containers=[], all=False):
        return self.__command(self.__create, containers=containers, all=all)

    def start(self, containers=[], all=False):
        return self.__command(self.__start, containers=containers, all=all)

    def stop(self, containers=[], all=False, time=docker.DOCKER_STOP_TIME):
        return self.__command(self.__stop, containers=containers, all=all, time=time)

    def remove(self, containers=[], all=False, time=docker.DOCKER_STOP_TIME, force=False):
        return self.__command(self.__remove, containers=containers, all=all, time=time, force=force)

    def restart(self, containers=[], all=False, time=docker.DOCKER_STOP_TIME):
        return self.__command(self.__restart, containers=containers, all=all, time=time)

    def stats(self, containers=[]):
        if not containers:
            try:
                containers = self.getDefinedServices()
            except Exception as e:
                return Fail(e)
        return self.__command(self.__stats, containers=containers)

    def status(self, containers=[]):
        if not containers:
            try:
                containers = self.getDefinedServices()
            except Exception as e:
                return Fail(e)
        return self.__readStates(containers) \
            .bind(self.__status, containers=containers)

    def reset(self, time=docker.DOCKER_STOP_TIME):
        managed = docker.readManagedContainers()
        if managed.isFail():
            return managed

        return managed \
            .bind(docker.filterExistingContainers) \
            .bind(docker.readContainersStatus) \
            .bind(self.__remove, containers=managed.getOK(), time=time, force=True)

    def pull(self, containers=[], all=False):
        if all:
            try:
                containers = self.getDefinedServices()
            except Exception as e:
                return Fail(e)

        registries = self.getRegistries()

        def pullImage(container):
            image = self.getContainerImage(container)
            unpacked = docker.unpackImageString(image)
            registry = unpacked.get('registry')
            op = OK(None)
            if registry and registry in registries:
                op.then(defer(self.login, registry=registry))
            return op.then(defer(docker.pull, image=image)) \
                .then(dinfo("'%s' (%s) has been pulled." % (container, image)))

        return Try.sequence(list(map(pullImage, containers)))

    def login(self, registry):
        registries = self.getRegistries()
        config = registries.get(registry)
        if not config:
            return Fail(InvalidRegistryError("Invalid registry specified for login. It is not configured."))
        logger.info("Logging into registry: %s" % registry)
        return docker.login(registry, config.get('username'), config.get('password'), config.get('email'))

    def recreate(self, containers=[], all=False, time=docker.DOCKER_STOP_TIME):
        if all:
            try:
                containers = self.getDefinedServices()
            except Exception as e:
                return Fail(e)
        return self.__readStates(containers) \
            .bind(self.__remove, containers=containers, force=True, time=time) \
            .then(defer(self.__readStates, containers=containers)) \
            .bind(self.__start, containers=containers)

    def run(self, container, containerArgs):
        jobs = self.getDefinedJobs()
        try:
            if container not in jobs:
                return Fail(InvalidContainerError("Container %s is not a defined job." % container))
        except Exception as e:
            return Fail(e)
        return docker.run(container, containerArgs, self.getJobConfig(container), basePath=self.getBasePath(), networks=self.getNetworks())

    def excmd(self, container, cmd, tty=False, interactive=False, user=None, detach=None, privileged=None):
        return self.__readStates([container]) \
            .bind(self.__exec, container=container, cmd=cmd, tty=tty, interactive=interactive, user=user, detach=detach, privileged=privileged)

    def __stats(self, state, containers=[]):
        existing = [x for x in containers if x in state]
        return docker.stats(existing)

    def __exec(self, state, container, cmd, tty=False, interactive=False, user=None, detach=False, privileged=False):
        if container not in state:
            return Fail(InvalidContainerError("'%s' does not exist. Cannot execute command." % container))
        if not state[container].running:
            return Fail(InvalidContainerError("'%s' is not running. Cannot execute command." % container))

        return docker.execmd(container, cmd, tty, interactive, user, detach, privileged)

    def __command(self, func, containers=[], all=False, *args, **kwargs):
        if all:
            try:
                containers = self.getDefinedServices(func, all)
            except Exception as e:
                return Fail(e)
        return self.__readStates(containers) \
            .bind(func, containers=containers, *args, **kwargs)

    def __readStates(self, containers):
        return self.readOrderedContainers(containers) \
            .bind(docker.filterExistingContainers) \
            .bind(docker.readContainersStatus)

    def __status(self, state, containers=[]):
        table = []
        for container in containers:
            if container not in state:
                status = docker.ContainerStatus(container)
            else:
                status = state[container]

            row = [
                container,
                status.getCol('cid'),
                status.getCol('pid'),
                status.getCol('ip'),
                dateToAgo(status.startedat) if status.startedat else "-",
                docker.getErrorLabel(status) if not status.running else "-"
            ]
            table.append(row)
        return OK(table)

    def __create(self, state, containers=[]):
        ops = []
        for container in containers:
            if container not in state:
                op = docker.create(container, self.getContainerConfig(container), basePath=self.getBasePath(), networks=self.getNetworks()) \
                    .then(dinfo("'%s' has been created." % container))
                ops.append(op)
            else:
                logger.warn("'%s' already exists." % container)
        return Try.sequence(ops)

    def __start(self, state, containers=[]):
        ops = []
        for container in containers:
            if container not in state:
                op = docker.create(container, self.getContainerConfig(container), basePath=self.getBasePath(),  networks=self.getNetworks()) \
                    .then(defer(docker.start, container=container)) \
                    .then(dinfo("'%s' has been created and started." % container))  \
                    .then(defer(self.writePid, container=container))
                ops.append(op)
            else:
                if not state[container].running:
                    op = docker.start(container) \
                        .then(dinfo("'%s' has been started." % container)) \
                        .then(defer(self.writePid, container=container))
                    ops.append(op)
                else:
                    logger.warn("'%s' is already running." % container)
        return Try.sequence(ops)

    def __stop(self, state, containers=[], time=docker.DOCKER_STOP_TIME):
        ops = []
        for container in containers:
            if container not in state:
                logger.warn("Container '%s' does not exist." % container)
            else:
                if state[container].running:
                    op = docker.stop(container, time) \
                        .then(dinfo("'%s' has been stopped." % container)) \
                        .then(defer(self.clearPid, container=container))
                else:
                    logger.warn("'%s' is not running." % container)
        return Try.sequence(ops)

    def __remove(self, state, containers=[], force=False, time=docker.DOCKER_STOP_TIME):
        logger.debug("REMOVE %s" % containers)
        ops = []
        for container in containers:
            if container in state:
                if state[container].running:
                    if not force:
                        logger.error(
                            "'%s' is running and 'force' was not specified." % container)
                    else:
                        op = docker.stop(container, time=time) \
                            .then(defer(docker.remove, container=container)) \
                            .then(dinfo("'%s' has been stopped and removed." % container)) \
                            .then(defer(self.clearPid, container=container))
                        ops.append(op)
                else:
                    ops.append(docker.remove(container).bind(
                        dinfo("'%s' has been removed." % container)))
        return Try.sequence(ops)

    def __restart(self, state, containers=[], time=docker.DOCKER_STOP_TIME):
        ops = []
        for container in containers:
            if container not in state:
                logger.error("'%s' does not exist." % container)
            else:
                if state[container].running:
                    op = docker.stop(container, time=time) \
                        .then(defer(docker.start, container=container)) \
                        .then(dinfo("'%s' has been restarted." % container)) \
                        .then(defer(self.writePid, container=container))
                    ops.append(op)
                else:
                    ops.append(docker.start(container)
                        .then(dinfo("'%s' has been started." % container))) \
                        .then(defer(self.writePid, container=container))

        return Try.sequence(ops)

    def getPidsConf(self):
        return self.config.get('pids', {})

    def getPidsDir(self):
        dir = self.getPidsConf().get('dir', '/var/run/dockwrkr')
        return expandLocalPath(dir, self.getBasePath())

    def arePidsEnabled(self):
        return self.getPidsConf().get('enabled', False)

    def writePid(self, container):
        if not self.arePidsEnabled():
            return OK(None)

        dir = self.getPidsDir()
        pidfile = os.path.join(dir, "%s.pid" % (container))

        return Shell.makeDirectory(dir) \
            .then(defer(docker.readContainerPid, container=container)) \
            .bind(defer(Try.attempt, writeToFile, filename=pidfile))

    def clearPid(self, container):
        if not self.arePidsEnabled():
            return OK(None)

        dir = self.getPidsDir()
        pidfile = os.path.join(dir, "%s.pid" % (container))

        if os.path.isfile(pidfile):
            return Try.attempt(os.remove, pidfile)
        else:
            return OK(None)
