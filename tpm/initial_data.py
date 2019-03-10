

#
# TRACKER INITIAL PRIORITY AND STATUS VALUES
#

from roundup import date

pri = db.getclass('priority')
pri.create(name=''"critical", order="1")
pri.create(name=''"urgent", order="2")
pri.create(name=''"bug", order="3")
pri.create(name=''"feature", order="4")
pri.create(name=''"wish", order="5")

stat = db.getclass('status')
stat.create(name=''"new", order="1")
stat.create(name=''"deferred", order="2")
stat.create(name=''"chatting", order="3")
stat.create(name=''"need-eg", order="4")
stat.create(name=''"in-progress", order="5")
stat.create(name=''"testing", order="6")
stat.create(name=''"done-cbb", order="7")
stat.create(name=''"resolved", order="8")

# create the two default users
user = db.getclass('user')
user.create(username="admin", password=adminpw,
    address=admin_email, roles='Admin')
user.create(username="anonymous", roles='Anonymous')

# add any additional database creation steps here - but only if you
# haven't initialised the database with the admin "initialise" command

partnertype = db.getclass('partnertype')
partnertype.create(name=''"Admin")
partnertype.create(name=''"ContentOwner")
partnertype.create(name=''"ProdHouse")

projecttype=db.getclass("projecttype")
projecttype.create(name="subtitling",shortname='SUB')
projecttype.create(name="dubbing",shortname='DUB')

language=db.getclass("language")
language.create(name="Hungarian", shortname="HU")
language.create(name="Czech", shortname="CZ")
language.create(name="Romanian", shortname="RO")
language.create(name="Bulgarian", shortname="BG")
language.create(name="Croatian", shortname="CR")

partner = db.getclass('partner')
partner.create(name=''"TPM",partnertype="Admin")
partner.create(name=''"Netflix",partnertype="ContentOwner")
partner.create(name=''"HBO", partnertype="ContentOwner")
partner.create(name=''"AltaMedia",partnertype="ProdHouse")
partner.create(name=''"Mediatranslations", partnertype="ProdHouse")

series = db.getclass('series')
series.create(title=''"Breaking Bad S01",client="Netflix")
series.create(title=''"Megborulva",client="HBO")

episode = db.getclass("episode")
episode.create(title="Pilot",series="1",duration=90,order=1,status='1',priority='4',deadline=date.Date('2019-02-01'))
episode.create(title="Cat's in the Bag...",series="1",duration=90,order=2,status='1',priority='4')
episode.create(title="...And the Bag's in the River",series="1",duration=90,order=3,status='1',priority='4')
episode.create(title="Cancer Man",series="1",duration=90,order=4,status='1',priority='4')
episode.create(title="Gray Matter",series="1",duration=90,order=5,status='1',priority='4')
episode.create(title="Crazy Handful of Nothin'",series="1",duration=90,order=6,status='1',priority='4')
episode.create(title="A No-Rough-Stuff-Type Deal",series="1",duration=90,order=7,status='1',priority='4')

project=db.getclass("project")
project.create(episode="1",language="CR",projecttype="SUB",supplier="4",status='new')
project.create(episode="1",language="HU",projecttype="DUB",supplier="4",status='new')
project.create(episode="1",language="CZ",projecttype="DUB",supplier="4",status='new')

tasktype=db.getclass("tasktype")
tasktype.create(name="Collect source files",shortname="csf")
tasktype.create(name="Production",shortname="prod")
tasktype.create(name="Quality Check",shortname="qc")
tasktype.create(name="Deliver localized content",shortname="dlc")

workflowname=db.getclass("workflowname")
workflowname.create(name="Simple Subtitling",shortname="ss")

workflow=db.getclass("workflow")
workflow.create(workflowname="ss",trg_type="2",trg_state='8',new_type='3',new_resp='1')
workflow.create(workflowname="ss",trg_type="3",trg_state='8',new_type='4',new_resp='1')

filetype=db.getclass("filetype")
filetype.create(name="script",shortname="script")
filetype.create(name="lowres",shortname="lowres")


# vim: set filetype=python sts=4 sw=4 et si
#SHA: f52a98b31599aa459a82a7852175660cf9cdcd6b
