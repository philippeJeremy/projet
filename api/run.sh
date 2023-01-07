docker run -it \
    -v "$(pwd):/home/app" \
    -p 4000:4000 \
    -e PORT=4000 \
    -e MLFLOW_TRACKING_URI="https://getaround-model.herokuapp.com/" \
    -e AWS_ACCESS_KEY_ID="AKIASH4B742BU5JXHT6E" \
    -e AWS_SECRET_ACCESS_KEY="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" \
    -e BACKEND_STORE_URI="postgresql://mjbrzzobdeavzz:c48765fdaa63b965b09b913b2f2356c9a3f34786d992695d49b0a74b6b7a26dd@ec2-18-215-96-22.compute-1.amazonaws.com:5432/dagrsjnnp8uf53" \
    -e ARTIFACT_ROOT="s3://model-bloc5/bloc5/" \
    test_api