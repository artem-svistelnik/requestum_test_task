# Requestum test task


**To start the project you need to execute:**

* clone project repo
* Create an .env file and populate it following the default.env file example, and be sure to create or add an existing hithub personal token.
* execute the command "make build"
* execute the command "make run"

**check the work:**

1)open in browser "http://0.0.0.0:8080/health"

if result is {"200":"ok"} then everything is correct

2)open in browser http://0.0.0.0:8080/contributors and check the work

P.S.: It can take a long time(5 seconds - few minutes) to load if there are many contributors to a given repository (If the loader is still running in the tab, the search is still running.)