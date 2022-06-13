
# -*- coding: utf-8 -*-
#import os
#from aiohttp import web
import logging
#from unittest.mock import MagicMock, patch
import asyncio
import numpy as np
from cbpi.api import *
from cbpi.api.base import CBPiBase

logger = logging.getLogger(__name__)


@parameters([Property.Actor(label="Actor01", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power01", description="Enter Power for Actor01 if Actors in group have different power."),
            Property.Actor(label="Actor02", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power02", description="Enter Power for Actor02 if Actors in group have different power."),
            Property.Actor(label="Actor03", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power03", description="Enter Power for Actor03 if Actors in group have different power."),
            Property.Actor(label="Actor04", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power04", description="Enter Power for Actor04 if Actors in group have different power."),
            Property.Actor(label="Actor05", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power05", description="Enter Power for Actor05 if Actors in group have different power."),
            Property.Actor(label="Actor06", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power06", description="Enter Power for Actor06 if Actors in group have different power."),
            Property.Actor(label="Actor07", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power07", description="Enter Power for Actor07 if Actors in group have different power."),
            Property.Actor(label="Actor08", description="Select an actor to be controlled by this group."),
            Property.Number(label="Power08", description="Enter Power for Actor08 if Actors in group have different power.")])

class GroupedPowerActor(CBPiActor):

    # Custom property which can be configured by the user
    @action("Set Power", parameters=[Property.Number(label="Power", configurable=True,description="Power Setting [0-100]")])
    async def setpower(self,Power = 100 ,**kwargs):
        self.power=int(Power)
        if self.power < 0:
            self.power = 0
        if self.power > 100:
            self.power = 100           
        await self.set_power(self.power)   

    def on_start(self):
        self.state = False
        self.actors = []
        self.maxactorpower = []
        self.powersum = []
        self.actorpower = []
        self.actorportion= []
        self.power = 100
        self.totalpower = 0
        logging.info("GROUPED POWER ACTOR")
        if self.props.get("Actor01", None) is not None:
            self.actors.append(self.props.get("Actor01"))
            self.maxactorpower.append(int(self.props.get("Power01",1)))
            self.totalpower = self.totalpower + self.maxactorpower[0]
        if self.props.get("Actor02", None) is not None:
            self.actors.append(self.props.get("Actor02"))
            self.maxactorpower.append(int(self.props.get("Power02",1)))
            self.totalpower = self.totalpower + self.maxactorpower[1]
        if self.props.get("Actor03", None) is not None:
            self.actors.append(self.props.get("Actor03"))
            self.maxactorpower.append(int(self.props.get("Power03",1)))
            self.totalpower = self.totalpower + self.maxactorpower[2]
        if self.props.get("Actor04", None) is not None:
            self.actors.append(self.props.get("Actor04"))
            self.maxactorpower.append(int(self.props.get("Power04",1)))
            self.totalpower = self.totalpower + self.maxactorpower[3]
        if self.props.get("Actor05", None) is not None:
            self.actors.append(self.props.get("Actor05"))
            self.maxactorpower.append(int(self.props.get("Power05",1)))
            self.totalpower = self.totalpower + self.maxactorpower[4]
        if self.props.get("Actor06", None) is not None:
            self.actors.append(self.props.get("Actor06"))
            self.maxactorpower.append(int(self.props.get("Power06",1)))
            self.totalpower = self.totalpower + self.maxactorpower[5]
        if self.props.get("Actor07", None) is not None:
            self.actors.append(self.props.get("Actor07"))
            self.maxactorpower.append(int(self.props.get("Power07",1)))
            self.totalpower = self.totalpower + self.maxactorpower[6]
        if self.props.get("Actor08", None) is not None:
            self.actors.append(self.props.get("Actor08"))
            self.maxactorpower.append(int(self.props.get("Power08",1)))
            self.totalpower = self.totalpower + self.maxactorpower[7]
        self.actornum=len(self.actors)
        #logging.info(self.actors)
        #logging.info(self.actornum)
        #logging.info(self.totalpower)
        #logging.info(self.maxactorpower)
        #self.actorportion=100*(float(1/self.actornum))
        i=0
        while i < self.actornum:
            self.actorportion.append(100*float(self.maxactorpower[i]/self.totalpower))
            if i == 0:
                power=self.actorportion[i]
            else:
                power=self.powersum[i-1]+self.actorportion[i]
            self.powersum.append(power)
            self.actorpower.append(0)
            i+=1
        logging.info(self.actorportion)
        logging.info(self.powersum)
        pass

    async def on(self, power=None):
        if power is not None:
            self.power = power
        self.calculate_individual_actor_power(self.power)
        i=0
        for actor in self.actors:
            await self.cbpi.actor.on(actor,self.actorpower[i])
            i+=1
        self.state = True
#        await self.cbpi.actor.actor_update(self.id,self.power)

    async def off(self):
        for actor in self.actors:
            await self.cbpi.actor.off(actor)
        self.state = False

    def get_state(self):
        return self.state

    async def set_power(self, power):
        self.power = power
        self.calculate_individual_actor_power(self.power)
        i=0
        for actor in self.actors:
            await self.cbpi.actor.set_power(actor,self.actorpower[i])
            i+=1

        await self.cbpi.actor.actor_update(self.id,self.power)
        pass

    def calculate_individual_actor_power(self, power):
        if int(power) > 100:
            power = 100
        if int(power) < 0:
            power = 0
        i=0
        self.actorpower=[]
        while i < self.actornum:
            self.actorpower.append(0)
            i+=1
        #logging.info(self.actorpower)
        idx = np.searchsorted(self.powersum, power, side="left")
        #logging.info(idx)
        #logging.info(self.powersum)
        max_actor_power=int(self.powersum[idx-1])
        #logging.info(max_actor_power)
        active_actor_power = round(100*power/max_actor_power)
        #logging.info(active_actor_power)
        if idx == 0:
            self.actorpower[0]=active_actor_power
        else:
            fixed_actor_power = int(self.powersum[idx-1])
            i=0
            while i < idx:
                self.actorpower[i]=100
                i+=1
            remaining_actor_power=power-fixed_actor_power
            variable_actor_power = round(100*remaining_actor_power/round(self.actorportion[i]))
            if int(variable_actor_power) > 100:
                variable_actor_power = 100
            if int(variable_actor_power) < 0:
                variable_actor_power = 0           
            self.actorpower[idx]=variable_actor_power

        #logging.info(self.actorpower)
        pass


    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("Grouped Power Actor", GroupedPowerActor)
    pass
