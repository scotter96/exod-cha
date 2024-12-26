Hello! Here's how you can install and use this module:

1. First you're gonna need a source install of Odoo 17 in your local machine to run the server locally (see https://www.odoo.com/documentation/17.0/administration/on_premise/source.html), please make sure you also have the basic configuration necessary to run Odoo.

2. Once it's up, open up a web browser and browse the localhost with the port you used for Odoo.

3. Then you should directed to a Database creation page. Otherwise, open the link below:
    http://localhost:<your_port>/web/database/manager
    example when using 8093 as Odoo's port:
    http://localhost:8093/web/database/manager

4. Then create a new database along with an administrator user access, and please check the Demo Data before proceeding.

5. After the database has been created successfully, go ahead and install the module from Odoo interface:
    - Go to the Apps menu.
    - Click on the "Update Apps List" button.
    - Search for "mrp_quality_workflow" and click "Activate".

6. Congrats! Now you've successfully installed the module. Now it's time to actually use it.
    Let's start by clicking the top-left grid button to show all the available modules, then click on the "Manufacturing" list in the dropdown.

7. You should now see some Manufacturing Order records in what we call a "List View", now you can go ahead and create a new one by clicking the "New" button on the top-left part of the screen beside the "Manufacturing Order" title.

8. Now let's try to manufacture a drawer by clicking on the Product field, and selecting "Drawer", it should shown as [FURN_8855] Drawer.

9. Once you're done, go ahead and click "Confirm"

10. Now you can notice in the "Quality Checks" tab, there are a few line records matching the line records in "Components" tab, now this is where the quality checking feature comes in.

11. But before that, under the "Components" tab, please tick the "Consumed" column for all components actually in use to make the Drawer.

12. So basically you have to check whether all Components needed to make a drawer are actually used correctly based on their quantity consumed during the manufacturing process. To do this, under "Quality Checks" tab, click on one of the record, and fill up the "Name" column with whatever tests name you might find suitable, and most importantly fill the "Tolerance Range" to determine how many quantity errors or gap between the real number checked physically and the ones in the Bills of Material are allowed in order for this Drawer to be passed QC.

13. Then fill the "Measured Value" with the real number checked physically, and the system will then automatically determines whether this component are passed or not in real time.

14. Now once every QC records are Passed, you can now click "Produce" or "Produce All".

15. Now if you have any Failed QC records, the MO status will change to On Hold, to advance, you need to click on "Restart Quality Check" and restart the whole QC process all over again.

16. Voila, now your Manufacturing process has a Quality Checking feature installed and ready to go.


Oh, and here's the command line to test the module functionality, including the PDF report.

python3 odoo-bin -c <config_file_if_any> -d <yoour_db_name> -u mrp_quality_workflow --test-enable --stop-after-init --log-level=test