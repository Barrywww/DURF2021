# DURF2021
Summer 2021 DURF project in mutation testing &amp; automated test generation fields.

Contributed by @Barry Wang, @ Harry Lee.

## Introduction

This project aims to provide a comprehensive testing solution for the manually injected faults in CSTP framework.

## Project Structure
The extendedPIT folder contains the customized mutator for PiTest framework and the field_matching_tool provides a NLP driven tool for semantic analysis on CSTP component fields and logs.
```
.
├── README.md
├── extendedPIT
│   ├── README.md
│   └── gregor
│       ├── config
│       └── mutators
└── field_matching_tool
    ├── DateSense
    ├── app.py
    ├── fieldItem.py
    ├── match_field_cn.py
    ├── match_rules.py
    ├── my_memory_translate.py
    ├── process_dict.py
    ├── process_test_suite.py
    ├── templates
    └── upload
```
