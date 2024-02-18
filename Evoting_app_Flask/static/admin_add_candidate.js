document.addEventListener('DOMContentLoaded', function () {
    var contract=new web3.eth.Contract(abi,address);
    const voteButtons = document.querySelectorAll('.btn-primary');
    voteButtons.forEach((button) => {
        button.addEventListener('click', async function () {
            try {
                // Request accounts from MetaMask
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                const account = accounts[0];

                const parameter = document.getElementById('name').value;
                const candidateDescription = document.getElementById('description').value;
                await contract.methods.addCandidate(parameter).send({ from: account });
                const endpointUrl = '/admin/add_candidate';
                const postData = {
                    name: parameter,
                    description: candidateDescription,
                };

                const requestOptions = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(postData),
                };
		console.log(requestOptions)
                const response = await fetch(endpointUrl, requestOptions);
                console.log(response)
                const responseData = await response.json();

                document.getElementById('name').value = '';
                document.getElementById('description').value = '';

                const successMessage = document.createElement('div');
                successMessage.classList.add('alert', 'alert-success', 'mt-3');
                successMessage.innerHTML = 'Candidate added successfully!';
                document.querySelector('.container').appendChild(successMessage);
            } catch (error) {
                console.error('Error adding candidate:', error);
            }
        });
    });
});
