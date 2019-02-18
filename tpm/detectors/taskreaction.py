
from roundup import roundupdb, hyperdb

def taskreaction(db, cl, nodeid, oldvalues):
    tasktype=cl.get(nodeid, 'tasktype')
    taskstatus=cl.get(nodeid,'status')
    taskproject=cl.get(nodeid,'project')
    taskepisode=cl.get(nodeid,'episode')

    for workflow_id in db.workflow.filter(None, {}):
        if tasktype==db.workflow.get(workflow_id,'trg_type'):
            if (taskstatus==db.workflow.get(workflow_id,'trg_state')) & (taskstatus!=oldvalues['status']):
                cl.create(project=cl.get(nodeid,'project'),
                          tasktype=db.workflow.get(workflow_id,'new_type'),
                          supplier=db.workflow.get(workflow_id,'new_resp') or db.project.get(cl.get(nodeid,'project'),'supplier'),
                          status='new')
    print "Tasktype:" + tasktype + "; Task status:" + taskstatus
    if (tasktype=="1") and (taskstatus=="8") and (oldvalues["status"]!="8"):
        print "Collect source files task resolved."
        files=cl.get(nodeid,'files')
        if db.episode.get(taskepisode,'files'):
            files=files+db.episode.get(taskepisode,'files')
        print "Adding " + str(files)
        db.episode.set(taskepisode,files=files)

def init(db):
    db.issue.react('set', taskreaction)

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 66d3581e42d879d9366734c6a523070a53e60894
