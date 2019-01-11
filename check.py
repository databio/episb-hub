
start = '40'
stop = 'A'

def check_start_stop(start,stop):
  # handle empty values
  if not start:
    print "I need a START vlaue"
    exit(1)
  if not stop:
    print "I need a STOP vlaue"
    exit(1)
  # check for non-numeric values
  if (start.isdigit() == False or stop.isdigit() == False):
    print "START and STOP must be numeric"
    exit(1)
  # check that stop is greater than start
  if (stopval <= startval):
    print "STOP value must be greater than START"
  else:
    print start + " is less than " + stop

check_start_stop(start,stop)

