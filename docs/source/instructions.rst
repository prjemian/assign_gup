Instructions for the Review Panel Chairman
==========================================

.. rubric:: Outline

.. TODO: revise here

#. Before the proposal deadline

	#. Determine the name of the next review cycle 
	   (something like ``2015-2``).
	   Change the value of ``APS_review_cycle`` 
	   (in :mod:`config`) to this value.
	#. `List of Reviewers`_
	#. Answer questions from review panel members.  CC the APS User Office.

#. After the proposal deadline

   #. `List of proposals`_
   #. `Reconfigure source code for next cycle`_
   #. Prepare the boilerplate letter
   #. Run the ``Assign_GUP`` software.

      #. `Assign topic weights to each proposal`_
      #. `Assign Reviewers to Proposals`_

   #. `Update the Assignments on the Web site`_
   #. `Send emails`_

List of Reviewers
~~~~~~~~~~~~~~~~~

.. sidebar:: At least a month before the GUP deadline...
   
   Check the reviewers and verify they all can attend on the review date.
   (GUP Calendar: http://www.aps.anl.gov/Users/Calendars/GUP_Calendar.htm)

#. Identify panel members whose terms expire soon.
#. Is a temporary reviewer necessary?
#. Identify new candidates to replace expiring panel members.
   Evaluate panel members strengths in the various topics for review
   and compare with proposal weights in each topic.  
   This will point out whether the panel has sufficient strength
   to review proposals on each topic.
#. Confirm the list of reviewers for the upcoming cycle.
#. Verify that each member can attend.
#. Assign values for reviewer strength on each topic.  
   Use a scale from 0 (no strength) to 1.0 (high strength), with 0.1 precision.


List of proposals
~~~~~~~~~~~~~~~~~

.. sidebar:: Be prompt! 

   Do this just after the proposal deadline.
   Assignments should be received within just a few days.
   Assigned reviewers must have sufficient to make their reviews.

#. Login to the Proposal review web site,
   (https://beam.aps.anl.gov/pls/apsweb/gup0008.panel_start_page?i_attrib=246B2411-PNL5),
   and click the "Download the list in XML" link.
   
     You might also consider using the "Print All Proposals" link
     to generate a single PDF file containing all the proposals and attachments.
     Any problem attachments will be noted on separate pages at the end of
     the document.
     Be sure to save that on-screen image to a file or it will go away 
     when you close your browser.
#. When that page appears, it will look unformatted and not like XML.  
   Don't worry, underneath the page is XML but is rendered poorly.
#. In your browser, choose "view source" (Control-U on Firefox)
   and save to a file such as ``raw-proposals-2015-2.xml`` (use the name of
   the proper review cycle).
#. This raw file may have characters that break the later XML processing.
   That's why I save it as raw and then make a working copy next.
#. Copy this file to ``proposals-2015-2.xml``
   and make one change first.  Add a ``period`` attribute to the root 
   element ``Review_list`` with a value of the current review cycle, such as::
   
     <Review_list period="2015-2">

Be on the lookout for:

* proposals that belong on another panel
* PUP or project proposals (they require additional reviewer work)
* identical or related proposals (may not be the same PI or beam line)
* ineligible reviewer(s) (ineligible since reviewer name is on the proposal)

Reconfigure source code for next cycle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: Refactor

   Try to make the source code immune to the simple reconfigurations
   necessary for each proposal review cycle.

As described above, Change the value of ``APS_review_cycle`` 
(in :mod:`config`) to the name of the next review cycle.  
Should be something such as ``2015-2``.

Assign topic weights to each proposal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to the reviewers, each proposal must be assigned a topic weight.
The weight (a floating point decimal number) is the relevance of each topic to the proposal.
The scale is 0 to 1 where 0 means *not related* and 1 mean *related*.

Assign Reviewers to Proposals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choose a primary and a secondary reviewer for each proposal.
Most likely, these will be reviewers with the strongest topic weighting
for this proposal.

Update the Assignments on the Web site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **XXXXXXXXXXXX** report gives a listing of the assigned reviewers for all proposals.
Looking at this page, enter the same information into the APS Review web site.
There is no upload capability possible for this data, you must enter it in from the web form.

Send emails
~~~~~~~~~~~

Send emails to each reviewer listing the proposals on which they
are primary or secondary reviewer.  CC the APS User Office 
on each email.
