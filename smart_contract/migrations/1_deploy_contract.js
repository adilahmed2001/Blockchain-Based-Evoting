const election_contract = artifacts.require("Election");

module.exports = function (deployer) {
  const election_name = "My Election";

  deployer.deploy(election_contract, election_name);
};
