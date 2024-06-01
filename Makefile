# Makefile

# Define the build target
build:
	@./scripts/build.sh
builddebug:
	@./scripts/debug-build.sh
testrun:
	@./scripts/testrun.sh
deploy:
	@kubectl apply -f deployment/deploy.yaml
teardown:
	@kubectl delete -f deployment/deploy.yaml
deploydebug:
	@kubectl apply -f deployment/deployment-debug.yaml
teardowndebug:
	@kubectl delete -f deployment/deployment-debug.yaml
