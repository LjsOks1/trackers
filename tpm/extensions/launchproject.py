from roundup.cgi.actions import Action
from roundup.anypy import urllib_
from roundup.cgi import exceptions, templating


class LaunchProject(Action):
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

        print props,links

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
