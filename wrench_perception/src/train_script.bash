export OUTDIR=Ball
export DIMX=24
export DIMY=24
export DIMIMGX=100
export DIMIMGY=100


function CascadeReady(){
	local GREEN_COLOR="$(echo -e "\E[1;32m")"
	local NO_COLOR="$(echo -e "\E[0m")"
	echo $GREEN_COLOR" -->  CascadeReady $OUTDIR"$NO_COLOR
	CascadeCD
	rm "samples_out$OUTDIR.vec" "bgp$OUTDIR.txt" "pos$OUTDIR.txt" "neg$OUTDIR.txt" -rf
	find "neg$OUTDIR" -iname "*.jpg" > "neg$OUTDIR.txt"
	cd "pos$OUTDIR"
	array=($(ls -1 | sort -r));
	for i in "${array[@]}"
	do
    		echo "pos$OUTDIR/$i" 1 0 0 "$DIMIMGX" "$DIMIMGY" >> ../"pos$OUTDIR.txt"
	done
	for i in "${array[@]}"
	do
    		echo "pos$OUTDIR/$i" 1 0 0 "$DIMIMGX" "$DIMIMGY" >> ../"pos$OUTDIR.txt"
	done
	cd ..
	export NUM_LINES=$(sed -n '$=' "pos$OUTDIR.txt")
	opencv_createsamples -num "$NUM_LINES" -w "$DIMX" -h "$DIMY" -info "pos$OUTDIR.txt" -vec "samples_out$OUTDIR.vec"
}

function CascadeShow(){
	local GREEN_COLOR="$(echo -e "\E[1;32m")"
	local NO_COLOR="$(echo -e "\E[0m")"
	echo $GREEN_COLOR" -->  CascadeShow $OUTDIR"$NO_COLOR
    CascadeCD
	export NUM_LINESP=$(sed -n '$=' "pos$OUTDIR.txt")
	echo $GREEN_COLOR"number of all positive samples = $NUM_LINESP"$NO_COLOR
    opencv_createsamples -w "$DIMX" -h "$DIMY" -vec "samples_out$OUTDIR.vec" -show
}

function CascadeTrain(){
	local GREEN_COLOR="$(echo -e "\E[1;32m")"
	local NO_COLOR="$(echo -e "\E[0m")"

	if [[ "$1" == "Clear" ]] ; then
		CascadeEmpty
	fi
	if [[ "$1" == "All" ]] ; then
		CascadeEmpty
		CascadeReady
	fi
	echo $GREEN_COLOR" -->  CascadeTrain $OUTDIR"$NO_COLOR
	CascadeCD
	export NUM_LINESP=$(sed -n '$=' "pos$OUTDIR.txt")
	NUM_LINESP=$((($NUM_LINESP*$4)/100))
	echo $GREEN_COLOR"Number of feeded positive samples = $NUM_LINESP"$NO_COLOR
	export NUM_LINESN=$(sed -n '$=' "neg$OUTDIR.txt")
	echo $GREEN_COLOR"Number of negative samples = $NUM_LINESN"$NO_COLOR
	date +"Start = - %a %b %e %H:%M:$S %Z %Y"
	opencv_traincascade -data "output$OUTDIR" -bg "neg$OUTDIR.txt" -vec "samples_out$OUTDIR.vec" -numPos "$NUM_LINESP" -numNeg "$NUM_LINESN" -w "$DIMX" -h "$DIMY" -mode ALL -precalcValBufSize 2048 -precalcIdxBufSize 2048 -numStages "$3" -featureType "$2"
	date +"Finish = - %a %b %e %H:%M:$S %Z %Y"
	cp "output$OUTDIR/cascade.xml" ../"cascade$OUTDIR.xml"
}