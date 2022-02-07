# CBPi4 Grouped Power Actor Plugin (Focus: Heating elements)

### This Actor plugin can be used to group up to 8 actors into on actor

## Group multiple actors into one actor
- This plugin allows to group up to 8 actors into one actor
- If the Grouped Actor is switched on, all actors that belong to the group will be switched on
- If the power is changed for the grouped actor, power will be adapted to the individual actors

## Current requirement
- All heating elements need to have the same nominal power. (e.g. 3 x 3 kW)
- Elements with different nominal power are not yet supported, but feasibility is planned

### Example
- You have 3 heating elements with 3 kW per element
- You have grouped all 3 heating elements into one grouped Power Actor
- You set the power for the grouped actor to 33% -> Element 1 of the grouped actor will heat with 100%
- You set the power of the grouped Actor to 50% -> Element 1 of the grouped actor will heat with 100% and Element 2 of the grouped actor will heat with 50% (pulsed or PWM)
- You set the power of the grouped Actor to 80% -> Element 1 and 2 of the grouped actor will heat with 100% and Element 3 will heat with ~ 40% (pulsed or PWM)
- All values between 0 and 100 can be used for the Grouped Power Actor
- Up to 8 Elements should work (3 have been tested so far)

### Installation:

You can install it directly via pypi.org:	
- sudo pip3 install cbpi4-GroupedPowerActor (no yet available on pypi.org)

Alternativeley you can install (or clone) it from the GIT Repo. In case of updates, you will find them here first:
- sudo pip3 install https://github.com/avollkopf/cbpi4-GroupedPowerActor/archive/main.zip

Afterwards you will need to activate the plugin:
- cbpi add cbpi4-GroupedPowerActor
	
- cbpi >= 4.0.0.45 from my fork is required. 

## Parameters:

- Actor 1-8: Actors can be added to the group

## Usage:

- You can add individual Actors to your dashboard
- Add the grouped Actor to your dashboard and enable actions to set power for the actor group

The grouped actor can be alo used in the Kettle Logic plugins that use power settings (e.g. PIDBoil,...)

Changelog:

- 07.02.22: (0.0.2) Initial commit 
