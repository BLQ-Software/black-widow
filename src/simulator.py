import simpy

def clock(env, name, tick):
    """Example clock simulation."""
    while True:
        print(name, env.now)
        yield env.timeout(tick)

env = simpy.Environment()
env.process(clock(env, 'fast', 0.5))
env.process(clock(env, 'slow', 1))
env.run(until=2)
