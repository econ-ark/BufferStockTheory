# reproduce.sh is a bash script that works on unix

## Windows does not natively handle symlinks. 

### Workarounds (thanks Claude):


1. Enable Developer Mode:
   Windows 10 (version 1703 and later) supports symlinks if you enable Developer Mode. Go to Settings > Update & Security > For developers and turn on Developer Mode.

2. Use Git with symlinks enabled:
   Configure Git to handle symlinks by running:
   ```
   git config --global core.symlinks true
   ```
   Then, clone your repository again.

3. Use Git Bash:
   Git Bash on Windows can handle symlinks better than the standard Windows command prompt.

4. Use WSL (Windows Subsystem for Linux):
   If you're on Windows 10, you can use WSL to work with your Git repository in a Linux environment.

5. Use junction points or directory symlinks:
   Windows supports junction points and directory symlinks. You can create these using the `mklink` command:
   ```
   mklink /D LinkName TargetPath
   ```

6. Use a third-party tool:
   Tools like Link Shell Extension can help create and manage symlinks on Windows.

7. Modify your code:
   If possible, modify your code to use relative paths instead of symlinks.

8. Use a post-clone script:
   Create a script that runs after cloning to create the necessary directory structure or copy files instead of using symlinks.

9. Use Git LFS (Large File Storage):
   For large files, consider using Git LFS instead of symlinks.

10. Use a virtual machine:
    If none of the above solutions work, you could run a Linux virtual machine on your Windows system to work with the repository.
