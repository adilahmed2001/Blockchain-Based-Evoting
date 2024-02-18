pragma solidity ^0.8.0;

contract Election {
    struct Candidate {
        string candidateName;
        uint256 voteCount;
    }

    struct Voter {
        bool isAuthorized;
        bool hasVoted;
        uint256 voteIndex;
    }

    address public contractOwner;
    string public electionTitle;

    mapping(address => Voter) public eligibleVoters;
    Candidate[] public candidateList;
    uint256 public totalVotesCast;

    modifier onlyOwner() {
        require(msg.sender == contractOwner, "Not the owner");
        _;
    }

    constructor(string memory _electionTitle) {
        contractOwner = msg.sender;
        electionTitle = _electionTitle;
    }

    function getCandidates() public view returns (Candidate[] memory){
        return candidateList;
    }
    function addCandidate(string memory _candidateName) public onlyOwner {
        candidateList.push(Candidate({candidateName: _candidateName, voteCount: 0}));
    }

    function getCandidateCount() public view returns (uint256) {
        return candidateList.length;
    }

    function authorizeVoter(address _voterAddress) public onlyOwner {
        eligibleVoters[_voterAddress].isAuthorized = true;
    }

    function castVote(uint256 _voteIndex) public {
        require(!eligibleVoters[msg.sender].hasVoted, "Already voted");
        require(eligibleVoters[msg.sender].isAuthorized, "Not authorized to vote");

        eligibleVoters[msg.sender].voteIndex = _voteIndex;
        eligibleVoters[msg.sender].hasVoted = true;
        candidateList[_voteIndex].voteCount += 1;
        totalVotesCast += 1;
    }

    function endElection() public onlyOwner {
        selfdestruct(payable(contractOwner));
    }
}
