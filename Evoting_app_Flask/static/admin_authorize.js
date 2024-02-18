document.addEventListener('DOMContentLoaded', function () {
    var contract=new web3.eth.Contract(abi,address);
    const authorizeButtons = document.querySelectorAll('.btn-primary');
    authorizeButtons.forEach((button, index) => {
        button.addEventListener('click', async function () {
            try {
                // Request accounts from MetaMask
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                const account = accounts[0];

                const parameter =  document.getElementsByClassName("address")[index].textContent;
                await contract.methods.authorizeVoter(parameter).send({from:account});
                console.log('authorized');
            } catch (error) {
                console.error('Error casting vote:', error);
            }
        });
    });
});