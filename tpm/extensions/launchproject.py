from roundup.cgi.actions import Action, EditCommon
from roundup.anypy import urllib_
from roundup.cgi import exceptions, templating
from roundup.exceptions import Reject, RejectRaw

class LaunchProject(EditCommon):
    def handle(self):
        ''' Perform some action. No return value is required.
        '''
        if self.client.env['REQUEST_METHOD'] != 'POST':
            raise Reject(self._('Invalid request'))
        # parse the props from the form
        try:
            props, links = self.client.parsePropsFromForm(create=1)
        except (ValueError, KeyError) as message:
            self.client.add_error_message(self._('Error: %s')
                % str(message))
            return
        print props
        print props[('project',self.form['projectid'].value)]['supplier']
        try:
            message = self._editnodes(props, links)
        except (ValueError, KeyError, IndexError, Reject) as message:
            escape = not isinstance(message, RejectRaw)
            self.client.add_error_message(
                self._('Edit Error: %s') % str(message), escape=escape)
            return
        self.db.project.set(self.form['projectid'].value,status='5') # Set project status to 'in-progress'
        #insert task(s)
        for task in self.db.workflow.filter(None,filterspec={'workflowname':'1', 'trg_type':None, 'trg_state':None}):
            t=self.db.issue.create(project=self.form['projectid'].value,
                                  tasktype=self.db.workflow.get(task,'new_type'),
                                  status='new',
                                  supplier=self.db.workflow.get(task,'new_resp') if self.db.workflow.get(task,'new_resp') else props[('project',self.form['projectid'].value)]['supplier'])
        # commit now that all the tricky stuff is done
        self.db.commit()

        # redirect to the item's edit page
        # redirect to finish off
        url = self.base + self.classname
        # note that this action might have been called by an index page, so
        # we will want to include index-page args in this URL too
        if self.nodeid is not None:
            url += self.nodeid
        url += '?@ok_message=%s&@template=%s'%(urllib_.quote('Project%s launched.' % (self.form['projectid'].value)),
            urllib_.quote(self.template))
        if self.nodeid is None:
            req = templating.HTMLRequest(self.client)
            print self.form['projectid'].value
            url += '&' + req.indexargs_url('', {})[1:]
        raise exceptions.Redirect(url)


def init(instance):
    instance.registerAction('launchproject', LaunchProject)
