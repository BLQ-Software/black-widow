# black-widow
TCP Network Simulator for Caltech CS 143.

## Quick set-up
#### Installing requirements
- ```pip install -r requirements.txt```
- (Can be installed to a virtualenv if desired)

#### Running the built-in simulator
- ```cd src; python run_simulator.py cases/case*.json -t Fast -n```

#### Writing your own simulator script
- ```>>> from blackwidow import BlackWidow```
- ```>>> settings = {'verbose': True}```
- ```>>> bw = BlackWidow(settings)```
- ```>>> bw.run('caseN.json')```

<br/>

## Full Documentation: 
- http://black-widow.readthedocs.org/


