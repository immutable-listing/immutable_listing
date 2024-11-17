listingDir=$1
mkdir deconstructed reconstructed
python segmentation_demo/deconstruct.py $listingDir deconstructed
python segmentation_demo/reconstruct.py $listingDir deconstructed reconstructed
python glue/listing_update.py reconstructed
echo -----------------------------------------------
python compare.py $listingDir/.listing_approved reconstructed/.listing_approved