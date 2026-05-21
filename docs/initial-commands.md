# Project Initialization Commands

These are the commands executed prior to resetting the master branch:

```bash
Microsoft Windows [Version 10.0.22631.4317]
(c) Microsoft Corporation. All rights reserved.

C:\Users\muzam\Documents\GitHub>git clone https://github.com/muzammil-13/ExamInsights_app.git
Cloning into 'ExamInsights_app'...
remote: Enumerating objects: 2643, done.
remote: Counting objects: 100% (2643/2643), done.
remote: Compressing objects: 100% (2474/2474), done.
remote: Total 2643 (delta 145), reused 2633 (delta 138), pack-reused 0
Receiving objects: 100% (2643/2643), 21.15 MiB | 13.57 MiB/s, done.
Resolving deltas: 100% (145/145), done.

C:\Users\muzam\Documents\GitHub>git checkout --orphan cleaned-history
fatal: not a git repository (or any of the parent directories): .git

C:\Users\muzam\Documents\GitHub>cd ExamInsights_app

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git stage
Nothing specified, nothing added.
hint: Maybe you wanted to say 'git add .'?
hint: Disable this message with "git config advice.addEmptyPathspec false"

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git init
Reinitialized existing Git repository in C:/Users/muzam/Documents/GitHub/ExamInsights_app/.git/

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git checkout --orphan cleaned-history
Switched to a new branch 'cleaned-history'

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git add -A

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git commit -am "the first commit"
[cleaned-history (root-commit) 0260128] the first commit
 12 files changed, 316 insertions(+)
 create mode 100644 .env
 create mode 100644 Dockerfile
 create mode 100644 Examinsights llm app working demo - Made with Clipchamp.gif
 create mode 100644 LICENSE
 create mode 100644 app.py
 create mode 100644 config.yaml
 create mode 100644 data/bsc-bca-3-sem-data-structure-using-cpp-22100730-apr-2022.pdf
 create mode 100644 data/sample-BCA_s4_dsa_Qs.pdf
 create mode 100644 project_structure.txt
 create mode 100644 readme.md
 create mode 100644 requirements.txt
 create mode 100644 streamlit_app.py

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git branch -D master
Deleted branch master (was a3075f4).

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git branch -m master

C:\Users\muzam\Documents\GitHub\ExamInsights_app>git push -f origin master
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (14/14), done.
Writing objects: 100% (15/15), 5.71 MiB | 675.00 KiB/s, done.
Total 15 (delta 0), reused 12 (delta 0), pack-reused 0
To https://github.com/muzammil-13/ExamInsights_app.git
+ a3075f4...0260128 master -> master (forced update)
```
