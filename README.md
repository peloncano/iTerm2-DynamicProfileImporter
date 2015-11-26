iTerm2-DynamicProfile
=====================

Script to import dynamic profile into iTerm2

I have a list of servers I would normally SSH into using iTerm. Managing this long list was a pain and manually organizing them in profiles was not an easy task.

Fortunately, iTerm2 `2.9.20140923 and later` allows for the creation of Dynamic Profiles.

[https://iterm2.com/dynamic-profiles.html](https://iterm2.com/dynamic-profiles.html)

This script was written to allow for simple creation of dynamic Profiles in iTerm2 for those individual hosts.

## Usage

Run the following to display the help manual

`python iterm_dynamic_profile_importer.py -h`

which looks like this:

```
usage: SCRIPT [-h] [-f FILENAME] [-i CSVIMPORT] [-r] [-t TAGS [TAGS ...]]
              [-l HOSTS [HOSTS ...]] [-c COMMAND]

This script will allow you to automatically create dynamic profiles for iTerm2
version 2.9.20140923 or later.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        Name of the dynamic profile plist file. File extension
                        is not required.
  -i CSVIMPORT, --import CSVIMPORT
                        CSV (comma separated) file. Two columns are accepted
                        for hostnames/ip address and tags.
  -r, --replace         If set the content of the dynamic profile will be
                        replaced/overwritten.
  -t TAGS [TAGS ...], --tags TAGS [TAGS ...]
                        Tag(s) to apply to the profile.
  -l HOSTS [HOSTS ...], --hosts HOSTS [HOSTS ...]
                        List of host names or IP addresses
  -c COMMAND, --command COMMAND
                        The custom SSH command to run. The host name should be
                        entered as '{host}'
```

The only required arguments are `-i` and `-l`

### Basic run!

#### CSV Sample

```
hostname-1, tag1 tag2 tag3
hostname-2, tag3 tag4 tag5
```
**Execute**

```
python iterm_dynamic_profile_importer.py -i /path/to/csv/file/above.csv
```

This will create a file in `~/Library/Application Support/iTerm2/DynamicProfiles` called `my-dynamic-profiles.plist`

Content of **_my-dynamic-profiles.plist_**:

```json
{
    "Profiles": [
        {
            "Command": "ssh hostname-1",
            "Custom Command": "Yes",
            "Guid": "hostname-1",
            "Name": "hostname-1",
            "Tags": [
                "tag1",
                "tag2",
                "tag3"
            ]
        },
        {
            "Command": "ssh hostname-2",
            "Custom Command": "Yes",
            "Guid": "hostname-2",
            "Name": "hostname-2",
            "Tags": [
                "tag3",
                "tag4",
                "tag5"
            ]
        }
    ]
}
```

New Dynamic Profiles can also be added by specifying the `-l` hostname argument:

```
python iterm_dynamic_profile_importer.py -l hostname-3 hostname-4 -t tag-5 tag-6 tag-7 -r
```

```javascript
{
    "Profiles": [
        {
            "Command": "ssh hostname-3",
            "Custom Command": "Yes",
            "Guid": "hostname-3",
            "Name": "hostname-3",
            "Tags": [
                "tag-5",
                "tag-6",
                "tag-7"
            ]
        },
        {
            "Command": "ssh hostname-4",
            "Custom Command": "Yes",
            "Guid": "hostname-4",
            "Name": "hostname-4",
            "Tags": [
                "tag-5",
                "tag-6",
                "tag-7"
            ]
        }
    ]
}
```

**NOTE: Running the script without specifying the `-r` argument will append to the current _my-dynamic-profiles.plist_. If `-r` is set, the old dynamic profiles will be wiped and the new ones added. Argument `-f` could've been set as well to output to a different file.***
