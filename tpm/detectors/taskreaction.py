
from roundup import roundupdb, hyperdb

def taskreaction(db, cl, nodeid, oldvalues):
    tasktype=cl.get(nodeid, 'tasktype')
    taskstatus=cl.get(nodeid,'status')
    taskproject=cl.get(nodeid,'project')
    for workflow_id in db.workflows.filter(None, {}):
        if tasktype==db.workflows.get(workflow_id,'trg_type'):
            if (taskstatus==db.workflows.get(workflow_id,'trg_state')) & (taskstatus!=oldvalues['status']):
                cl.create(project=cl.get(nodeid,'project'),
                          tasktype=db.workflows.get(workflow_id,'new_type'),
                          supplier=db.workflows.get(workflow_id,'new_resp') or db.project.get(cl.get(nodeid,'project'),'supplier'),
                          status='new')






def init(db):
    db.issue.react('set', taskreaction)

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 66d3581e42d879d9366734c6a523070a53e60894
