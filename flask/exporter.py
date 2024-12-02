import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location","Link"])

  for job in jobs:
    writer.writerow(list(job.values())) 
    #dictionary는 값만 불러올 수 있음
    #query argument는 ? 뒤에 있는 것
   
  return