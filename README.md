# Passcrypt Safe Rework : Alternative
- A rework of an old project called Passcrypt Safe to learn basic implementation of password management
- Mainly for educational purposes (building a system, building a basic database, basic encryption / decryption function utilization) and not for actual password storage.

# Differences from original project
- Structure is more focused on readability and ease of expanding the program
- Usage of sqlite
- Usage of cryptography.Fernet
- No GUI interface

# Status
- Work-In-Progress, but working in the basic sense
  - Adjustments to src functions and interface development will be in future commits
    - Adjustments are focused on being able to expand the program
  - Experimentation is being done with finding ways to expand the program through a plugin-esque method

# Should this be used for password storage?
- With enough customization and development, this can be a proper personal password manager
  - But this requires not releasing such customized code in public, unless there are security measures that assure system security

# How to Install Dependencies (WIP)
- Mainly sqlite 3 and bcrypt are the main dependencies so far
- WIP : Will be filled up at some point

# How to Use (WIP)
- open the main.py file
  - configure DEBUG to 0 for the main program
  - configure DEBUG to 1 for the alternative note encryption program (expansion experiment)
- run the main.py file
- follow prompt instructions