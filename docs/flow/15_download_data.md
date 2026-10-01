# 15_download_data

Source: https://support.google.com/flow/answer/17571126?hl=en

Download your Google Flow data
You can export and download a copy of your Google Flow data to back it up or use it with another service.
Important: Downloading your data doesn't delete it from Google servers. Learn how to delete your Flow projects.
What data is exported
You can export Google Flow content you have created, uploaded, or generated in Google Flow.
Generated and uploaded media: Your images, videos, and audio files.
Prompts and generation settings: Text prompts, requested aspect ratios, AI model names, camera controls, voice configurations, and video trim offsets.
Project and folder organization: Projects, collections, nested folder hierarchies, and favorite tags.
Characters and scenes: Character personality notes, character definitions, scenes, aspect ratios, and clip sequences.
Edit stacks: Ordered generation history showing edit prompts and version chains.
Step 1: Select your Google Flow Data
Go to takeout.google.com.
Make sure to sign in to the same Google Account that you use for Flow.
Your data from most Google products and services is included in the export by default. This includes Flow.
Under "Select data to include," select Deselect all.
Under "Create a new export," locate Flow in the product list.
Check the box next to Flow.
Scroll down and click Next step.
Step 2: Customize your export options
After you select your Flow data, choose how you want to receive your archive and its format.
Part 1: Choose how to get your data
Part 2: Choose the export frequency
Part 3: Choose the file type & max size of your archive
Step 3: Get your Google Flow Data Archive
Click Create export.
Google Takeout will begin processing your archive.
Tip: Depending on the volume of media and video generations in your account, exports can take anywhere from a few minutes to several hours.
When the export is ready, you will receive an email notification.
Open the email and click Download archive (or go to "Manage exports" on Google Takeout).
Unzip or extract the downloaded file on your computer to view your Google Flow files.
Step 4: Understand your Google Flow Data
When you unzip your download, your Google Flow data is organized into two  main areas:
Structure & Timeline JSON files: Located in the main folder, files like projects.json, collections.json, characters.json, scenes.json, and edit_stacks.json.
The media/folder: All generated or uploaded images (.jpg), videos (.mp4), and audio (.wav) are saved in one central media/folder.
Paired metadata: Every media file is paired with an adjacent JSON file sharing the exact same ID (e.g., abc123.mp4 and abc123_metadata.json). These metadata files store generation prompts, aspect ratios, model names, and reference assets.
Tip: In Google Flow, you organize media in nested projects and collections. In your Takeout download, all media files are saved together in the download folder using unique ID numbers. To see which project or collection a file belongs to, open its corresponding _metadata.json file.
Fix issues with your export
Your export failed or is taking a long time
Large media files: Archives containing long video renders can take a long time to generate. If an export fails or times out, try selecting a smaller file split size (such as 2 GB) in Step 2.
Download expiration: Takeout download links are active for 7 days. After 7 days, you will need to request a new export.
Your export is missing files
Multiple accounts: Verify that you signed into the specific Google Account used when creating content in Google Flow.
Unique file names: Google Flow uses unique internal IDs (media_id, project_id) rather than display names to name exported files. This prevents file overwrites if multiple projects share identical display names (such as "Untitled Project"). Search the JSON metadata files to map IDs back to display titles.
Learn more about Google Takeout
For more info about Google Takeout, answers to common questions, and more, review the Google Takeout article.
Give feedback about this article
Help
Get started with Google Flow
Use the Google Flow Agent
Create videos in Google Flow
Edit videos & build scenes in Google Flow
Create & edit images in Google Flow
Create & use your avatar in Google Flow
Create & manage Tools in Google Flow
Manage your Google Flow projects, assets & collections
Learn about Google Flow models & supported features
Manage your Google Flow credits
Where you can use Google Flow
Report a problem or send general feedback
Manage your data in Google Flow
Use keyboard shortcuts in Google Flow
Download your Google Flow data
