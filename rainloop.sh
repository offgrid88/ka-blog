mkdir rainloop
cd rainloop

curl -s http://repository.rainloop.net/installer.php | php


cd ..

sudo mv rainloop /var/www/

sudo chown www-data:www-data /var/www/rainloop/ -R

sudo nano /etc/apache2/sites-available/rainloop.conf


