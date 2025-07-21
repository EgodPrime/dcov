
all: dcov_agent

dcov_agent: src/main/java/com/kb310/dcov/*.java
	mvn package

.PHONY: install
install:
	cp target/dcov-1.0-SNAPSHOT-jar-with-dependencies.jar /usr/lib/dcov_agent.jar

.PHONY: clean
clean:
	mvn clean

.PHONY: uninstall
uninstall:
	rm /usr/lib/dcov_agent.jar