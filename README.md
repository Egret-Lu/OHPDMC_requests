# OHPDMC_requests


stalist file -- all station list with net + station +start time+end time. This is get from the OHPDMC website which includes the observation time range of all station. Station of different network has been put in different csv file as the request will  have some difference.

1. Step 1: requst-[network].py -- Here we send request to the institution automatically. **You should substitute my email and password first** . Highly recommend you register a new outlook email as there will be a large amount of data.

2. Step 2: dataDownloadxx.py -- get the url link of all seedlist file which has send to your email box. Save them to seedlist.txt

3. Step 3: wgetJob.py -- use parallel task to download all seed  in seedlist.txt. This will run on bluehive

* p.s.: rej.Recover.py -- some requests may fail so. You can use this to send request again (also they may fail again but just don't care. That is normal case

Hope my old code can help you anyway^_^
