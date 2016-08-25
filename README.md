# Eventit

## Intro
Eventit is an EMS (Event Management System), which is a software that allows the user to make CRUD actions over event records. It also allows other users to mark their attending to those events and to receive information about them.
 
It has been developed for being highly customizable using templates, configuration files, and several engines for managing asset storing, mailing...
 
## How to start using (coding) it?

At this point Eventit is in development phase and not usable. However to install it is pretty easy: clone this repository and install dependences:  
```
$ pip install -r requirements.txt
```

If you are going to add code on it you also need to install the dev dependences:
```
$ pip install -r requirements_dev.txt
```

Now you'll need to (1) add a default config file, (2) configure database, and (3) add test data.
```
$ python manage write_config
$ python manage setup_db
$ python manage generate_test_data
```

Steps 2 and 3 can be performed in only one command with:
```
$ python manage prepare_dev
```

## How to add an admin user (with name 'admin')?
```
$ python manage create_admin -n admin
```

## How to run a dev server?
```
$ python manage runserver
```