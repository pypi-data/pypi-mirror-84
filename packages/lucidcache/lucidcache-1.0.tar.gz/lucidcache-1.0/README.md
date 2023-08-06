# LucidCache
Simple Python library for caching functions' output

## Installation
### Installation from PyPi repository:
1. Download and install Python 3 from the [official website](https://www.python.org)
2. Type the following command in order to install the library:
```
pip3 install lucidcache
```

### Installation from source code:
1. Download and install Python 3 from the [official website](https://www.python.org)
2. Download and install Git from the [official website](https://git-scm.com/)
3. Type the following commands in Git Bash console in order to install the library:
```
git clone https://github.com/Kaletise/LucidCache.git
cd LucidCache
py setup.py install
```

## Examples
* Caching SQL queries is as simple as one decorator:
```
# By using the lucidcache.cacheable decorator, we make the function get_user cacheable
# As soon as it's called, its return will be cached
# When this function is called with exactly the same parameters later, it will return
# previously cached return and won't spend any time to execute needless SQL query
@lucidcache.cacheable
def get_user(username):
    connection = database.connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
    user = cursor.fetchone()
    connection.close()
    return user

# This function is cacheable, too
@lucidcache.cacheable
def get_users():
    users = []
    connection = database.connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    for user in cursor.fetchall():
        users.append(user)
    connection.close()
    return users

# As soon as this function is called, the decorator lucidcache.nocache will clear
# the cache of the functions get_user and get_users in order for data to stay up-to-date
@lucidcache.nocache(get_user, get_users)
def add_user(username, password):
    connection = database.connect()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (%s, %s)', (username, password))
    connection.commit()
    connection.close()
```
* More examples are coming (probably)

## LICENSE
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Any contribution is appreciated!