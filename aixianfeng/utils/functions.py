import random, time


def get_ticket():
    s = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ticket = ''
    for _ in range(32):
        ticket += random.choice(s)
    t = time.time()
    ticket = 'TK' + ticket + str(int(t))
    return ticket