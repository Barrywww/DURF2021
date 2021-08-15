# Readme

## Overview
This expanded mutator is specifically designed to match patterns in CSTP framework. Based on the work of PiTest, with Gregor mutation engine.

## Build Dependencies
```
JDK >= 11.0
pitest >= 1.6.8
```

## Files and Locations
Simply replace the files in this git repo as the following tree shows. The mutator is registered as `REMOVE_CSTP_PATTERN` in `Mutators.java`

```
org.pitest.mutationtest.engine.gregor
├── config
│   └── Mutator.java
└── mutators
    └── experimental
        └── PatternMatchMutator.java
```

## Sample Configuration
This is a sample configuration in the TARGET project. By doing the configuration below, it will enable PiTest to apply the mutator in `pitest:report` and `pitest:mutationCoverage` goals.
```
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>{BUILD_VERSION}</version>
    <configuration>
        <targetClasses>
            <param>{TARGET_CLASS}</param>
        </targetClasses>
        <targetTests>
            <param>{TEST_CLASS}</param>
        </targetTests>
        <verbose>true</verbose>
        <mutators>
            <mutator>REMOVE_CSTP_PATTERN</mutator>
        </mutators>
    </configuration>
</plugin>
```