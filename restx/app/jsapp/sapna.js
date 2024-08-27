async function generateImage() {
    const prompt = document.getElementById('promptInput').value;
    const outputDiv = document.getElementById('output');

    outputDiv.innerHTML = '<p class="text-gray-600">Generating image...</p>';

    try {
        const response = await axios.post('http://127.0.0.1:5000/sapna', {
            prompt: prompt
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        });

        const imageBase64 = response.data.image;
        outputDiv.innerHTML = `<img src="data:image/png;base64,${imageBase64}" alt="Generated Image" class="max-w-full h-auto rounded-md shadow-md">`;
    } catch (error) {
        console.error('Error:', error);
        outputDiv.innerHTML = '<p class="text-red-500">Error generating image. Please try again.</p>';
    }
}
