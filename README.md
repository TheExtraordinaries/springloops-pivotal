# springloops-pivotal

This is a basic python module and light webapp inspired by jujhars13's [Springloops and Pivotal Integration](https://github.com/jujhars13/springloops-and-PivotalTracker-Integration) that will log commit messages tagged with the pivotal story id or the link to the story in the commit message to the relevant story.

## Commit Syntax
The module is a simple wrapper for the [source_commits](https://www.pivotaltracker.com/help/api/rest/v5#Source_Commits) api endpoint provided by pivotal. All of the source_commits syntax (e.g. tagging a story within brackets like ` [fixed #1234567]`) will work.

Additionally, this module will format links to stories in the form `https://www.pivotaltracker.com/story/show/<story_id>` into the appropriate syntax for the source_commits endpoint.

One quirk of the springloops webhook is that commit messages with empty lines will be truncated on that empty line. In light of this, for now this module will only work with commit messages that do not have an empty line in them.

## Installation
This respoitory holds a very simple example [Flask](http://flask.pocoo.org/) app that can be run as its own standalone app. However, integrating this with an existing python web app is simple, first `import pusher` in the function that you point the springloops webhook (pusher is in the flask_application directory), then send the form parameters to the pusher module: `pusher.pushToPivotal(request.form)`.

The full example can be found in the flask_application/dispatch.py file:

    import pusher
    
    @app.route('/newcommit', methods=['POST'])
    def newcommit():
        result = pusher.pushToPivotal(request.form)
    
        resp = jsonify({"success": result})
        resp.status_code = 200
    
        return resp
        
Note that the pusher module has one requirement: the [Requests](http://requests.readthedocs.org/en/latest/) module.

After adding the module, simply point a springloops 'commit' webhook to your url.
