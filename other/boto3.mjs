/* 
V2: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/getting-started-nodejs.html
V3: https://aws.amazon.com/es/sdk-for-javascript/

https://huggingface.co/openai/whisper-tiny
https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&language=es,en&sort=trending
https://huggingface.co/docs/transformers.js/api/pipelines#module_pipelines.AutomaticSpeechRecognitionPipeline
https://huggingface.co/docs/transformers.js/guides/node-audio-processing
*/


import {
  ListObjectsCommand,
  GetObjectCommand,
  S3Client,
} from "@aws-sdk/client-s3";
import { Readable } from "stream";
import fs from "fs";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

import { pipeline } from "@xenova/transformers";
import wavefile from "wavefile";
import fetch from "node-fetch";

const client = new S3Client({
  region: "us-east-1",
});

const bucketName = "tnknbucket";
const command = new ListObjectsCommand({ Bucket: bucketName });

const getObject = async () => {
  try {
    // const { Body } = await client.send(
    //   new GetObjectCommand({
    //     Bucket: bucketName,
    //     Key: "audio/recorded_audio.wav",
    //   })
    // );
    // console.log(Body);

    // get signed URL of the object
    const command = new GetObjectCommand({
      Bucket: bucketName,
      Key: "audio/recorded_audio.wav",
    });

    // No funciona porque el audio grabado desde el navegador tiene un formato diferente
    let url = await getSignedUrl(client, command, { expiresIn: 3600 });
    console.log(url);

    url = "https://huggingface.co/datasets/Xenova/transformers.js-docs/resolve/main/jfk.wav";
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`unexpected response ${response.statusText}`);
    }
    // console.log(response);
    let buffer = Buffer.from(await fetch(url).then((x) => x.arrayBuffer()));
    console.log(buffer);

    let wav = new wavefile.WaveFile(buffer);
    wav.toBitDepth("32f"); // Pipeline expects input as a Float32Array
    wav.toSampleRate(16000); // Whisper expects audio with a sampling rate of 16000
    let audioData = wav.getSamples();
    if (Array.isArray(audioData)) {
      if (audioData.length > 1) {
        const SCALING_FACTOR = Math.sqrt(2);

        // Merge channels (into first channel to save memory)
        for (let i = 0; i < audioData[0].length; ++i) {
          audioData[0][i] =
            (SCALING_FACTOR * (audioData[0][i] + audioData[1][i])) / 2;
        }
      }

      // Select first channel
      audioData = audioData[0];
    }

    const transcriber = await pipeline(
      "automatic-speech-recognition",
      "Xenova/whisper-tiny.en"
    );

    let start = performance.now();
    let output = await transcriber(audioData, {
      // language: "spanish",
      return_timestamps: true,
      // task: "transcribe",
    });
    let end = performance.now();
    console.log(`Execution duration: ${(end - start) / 1000} seconds`);

    console.log(output);

    // // Read the stream and convert it to bytes
    // // If uncoomment the next 2 lines before, the stream will be consumed and the next code will fail
    // const data = await streamToBuffer(Body);
    // console.log(data);

    // // Create a writable stream to the file
    // const writableStream = fs.createWriteStream("recorded_audio.wav");

    // // Pipe the S3 stream to the file stream
    // Body.pipe(writableStream);

    // // Wait for the write operation to finish
    // await new Promise((resolve, reject) => {
    //   writableStream.on("finish", resolve);
    //   writableStream.on("error", reject);
    // });

    // console.log("WAV file saved successfully.");
  } catch (error) {
    console.error(error);
  }
};

getObject();
