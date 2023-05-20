from chat import getTag, getReplyFromTag

while True:
    message = input('You: ')
    tag = getTag(message)
    if tag == 'goodbye':
        print('Nuzat: ', getReplyFromTag(tag) )
        print('Shutting down self.')
        break
    else:
        if tag == 'sendEmail':
            print('Nuzat: Sorry I do not have that power right now.')
        elif tag == 'cancelMail':
            print('Nuzat: There is no email to be send.')
        else:
            print('Nuzat: ', getReplyFromTag(tag) )
