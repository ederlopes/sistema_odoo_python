CREATE USER odoo SUPERUSER INHERIT CREATEDB CREATEROLE;
ALTER USER odoo PASSWORD 'odoo';
DROP DATABASE sce;
