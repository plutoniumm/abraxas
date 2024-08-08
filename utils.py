def what(o):
  return [i for i in dir(o) if not i.startswith('_')]

def whatall(o):
  return [i for i in dir(o)]