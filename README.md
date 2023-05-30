# OHPDMC_requests


Here is the file you need to focus on (others maybe some out-time code or some code complete by other researcher:

stalist file -- all station list with net + station +start time+end time. This is get from the OHPDMC website which includes the observation time range of all station. Station of different network has been put in different csv file as the request will  have some difference.

1. Step 1: requst-[network].py -- Here we send request to the institution automatically,request will ask data of each station seperately (5 days one time or they will refuse your requests). **You should substitute my email and password first** . Highly recommend you register a new outlook email as there will be a large amount of data.

2. Step 2: dataDownloadxx.py -- get the url link of all seedlist file which has send to your email box. Save them to seedlist.txt

3. Step 3: wgetJob.py -- use parallel task to download all seed  in seedlist.txt. This will run on bluehive. Currently 20 seed file as a group. Then put the file on the bluehive and submit the task.

* p.s.: rejRecover.py -- some requests may fail so. You can use this to send request again (also they may fail again but just don't care. That is normal case

Hope my old code can help you anyway ^_^
