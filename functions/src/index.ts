import { onRequest } from "firebase-functions/v2/https";
import Replicate from "replicate";


// https://firebase.google.com/docs/functions/typescript

export const helloWorld = onRequest(async (request, response) => {
    console.log(request.body)
    const apiKey = "r8_QhZyLPYKv5E3kXAUoMNY2GKW9qszc7o3eZouA"

    const replicate = new Replicate({
        auth: apiKey,
    });

    const model = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4";
    const input = {
        prompt: "coloring book",
        image: request.body.img,
    };
    const output = await replicate.run(model, { input });


    response.set('Access-Control-Allow-Origin', '*')
    response.status(200).send(output);
});
