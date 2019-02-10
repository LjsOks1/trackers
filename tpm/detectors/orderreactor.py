from roundup import date
import csv
import logging
from cStringIO import StringIO
import sys
import traceback

log_stream=StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO)

def processorder(db, cl, nodeid, oldvalues):
    ''' For now let's just process the order files received from HBO....
    '''
    if cl.get(nodeid,'files'):
        if oldvalues and oldvalues['files']:
            new_file= [x for x in cl.get(nodeid,'files') if x not in oldvalues['files']]
        else:
            new_file=cl.get(nodeid,'files')
        if new_file:
            try:
                logging.info("Processing file:"+db.file.get(new_file[0],'name'))
                content=db.file.get(new_file[0],'content')
                csv_reader=csv.DictReader(content.splitlines()[1:])
                for row in csv_reader:
                    print(row)
                    if not db.episode.filter(None,{'title':row['Title']}):
                        episode_id=db.episode.create(title=row['Title'],
                                                    duration=int(float(row['Length'])),
                                                    barcode=row['Barcode'],
                                                    screenerid=row['Screener Id'],
                                                    deadline=date.Date(row['Deadline']),
                                                    client=cl.get(nodeid,'partner'))
                        logging.info('%s ... Episode%s created' % (row['Title'], episode_id))
                    else:
                        episode_id=db.episode.filter(None,{'title':row['Title']})
                        logging.info('%s ... Episode%s exists, creation skipped.' % (row['Title'], episode_id))
                    if not db.project.filter(None,{'episode':episode_id,
                                                'supplier':cl.get(nodeid,'partner'),
                                                'projecttype':row['Category'],
                                                'language':row['Language'] }):
                        project_id=db.project.create(episode=episode_id,
                                                    supplier=cl.get(nodeid,'partner'),
                                                    projecttype=row['Category'],
                                                    language=row['Language'],
                                                    order=nodeid)
                        logging.info('%s ... Project%s created' % (row['Title'], project_id))
            except Exception as e:
                logging.error(traceback.format_exc())
            msg={}
            msg['content']=log_stream.getvalue()
            msg['date']=date.Date('.')
            msg['author']=str(db.getuid())
            msg_id=db.msg.create(**msg)
            all_messages=[msg_id]
            if cl.get(nodeid,'messages'):
                all_messages=all_messages+cl.get(nodeid,'messages')
            cl.set(nodeid,messages=all_messages)

def init(db):
    # fire before changes are made
    db.order.react('create', processorder)
    db.order.react('set', processorder)

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 4dc3c37fa69612010a9684a544585aabe836bf35
