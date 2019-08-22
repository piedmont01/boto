from functools import wraps

def my_logger(orig_func):
  import logging
  logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)

  @wraps(orig_func)
  def wrapper(*args, **kwargs):
    logging.info(
      'Ran with args: {} and kwargs: {}'.format(args,kwargs))
    return orig_func(*args, **kwargs)
  return wrapper

@my_logger
def display_info(name, age):
  print('display_info ran with arguments ({},{})'.format(name,age))

display_info('John', 25)
