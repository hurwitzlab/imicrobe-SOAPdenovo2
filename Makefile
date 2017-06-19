APP=imicrobe-SOAPdenovo2
VERSION=0.0.1
EMAIL=mbomhoff@email.arizona.edu

files-delete:
	files-delete $(CYVERSEUSERNAME)/applications/$(APP)-$(VERSION)

files-upload:
	files-upload -F stampede/ $(CYVERSEUSERNAME)/applications/$(APP)-$(VERSION)

apps-addupdate:
	apps-addupdate -F stampede/app.json

test:
	sbatch test.sh

jobs-submit:
	jobs-submit -F stampede/job.json

container:
	rm -f singularity/$(APP).img
	sudo singularity create --size 512 singularity/$(APP).img
	sudo singularity bootstrap singularity/$(APP).img singularity/$(APP).def

iput-container:
	irm $(APP).img
	iput -K singularity/$(APP).img

iget-container:
	iget -K $(APP).img
	mv $(APP) stampede/
