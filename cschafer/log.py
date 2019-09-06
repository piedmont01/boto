import logging
logging.basicConfig(filename='example.log', level=logging.INFO)

def logger(func):
  def log_func(*args):
    logging.info('Running "{}" with arguemnts {}'.format(func.__name__,args))
  return log_func

def add(x,y):
  return x+y

def sub(x,y):
  return x-y


add_logger = logger(add)
sub_logger = logger(sub)

add_logger(3,3)
sub_logger(4,5)

