pragma ton-solidity >= 0.35.0;
pragma AbiHeader time;
pragma AbiHeader expire;

contract tonFile {
    uint public value;
    uint constant ERROR_NO_WALLET = 100;
    uint constant ERROR_NO_PUBKEY = 101;
    uint constant ERROR_SENDER_IS_NOT_MY_OWNER = 102;
    uint constant ERROR_NO_ROOT_ADDRESS = 103;
    uint constant ERROR_CHUNKS_COUNT_MUST_BE_ABOVE_THAN_ZERO = 104;

    uint constant ERROR_UPLOAD_IN_PROCCESS = 105;
    uint constant ERROR_INCORRECT_INDEX = 106;
    uint constant ERROR_CHUNK_ALREADY_EXISTS = 107;
    uint constant ERROR_INCORRECT_CHUNKS_COUNT = 108;
    uint constant ERROR_SENDER_IS_NOT_ALLOWED = 109;

    // State:
    uint64 static nonce;
    uint32 m_chunks_count;
    uint32 m_cur_chunk_count;
    string _mime;
    string _extension; // only string after dot
    address allowance_dest;

    bytes[] public m_raw_data_chunks;

    constructor(uint32 chunks_count, string mime, string extension) public {
        require(tvm.pubkey() != 0, 101);
        require(chunks_count > 0, ERROR_CHUNKS_COUNT_MUST_BE_ABOVE_THAN_ZERO);
        tvm.accept();
        
        m_chunks_count = chunks_count;
        m_raw_data_chunks = new bytes[](m_chunks_count);
        _mime = mime;
        _extension = extension;
    }

    modifier onlyOwnerAndAccept {
        require(msg.pubkey() == tvm.pubkey(), 102);
        tvm.accept();
        _;
    }

    function writeData(uint32 index, bytes chunk) public onlyOwnerAndAccept{
        require(msg.pubkey() == tvm.pubkey(), ERROR_SENDER_IS_NOT_MY_OWNER);
        require(m_raw_data_chunks[index].length == uint(0), ERROR_CHUNK_ALREADY_EXISTS);
        require(index <= m_chunks_count, ERROR_INCORRECT_INDEX);
        require(m_cur_chunk_count <= m_chunks_count, ERROR_INCORRECT_CHUNKS_COUNT);
        tvm.accept();

        m_raw_data_chunks[index] = chunk;

        ++m_cur_chunk_count;
    }

    function afterSignatureCheck(TvmSlice body, TvmCell message) private inline returns (TvmSlice) {
        body.decode(uint64);
        uint32 expireAt = body.decode(uint32);
        require(expireAt >= now, 101);
        return body;
    }
    function getDetails() public view returns (uint128 chunks_count, uint128 cur_chunk_count, uint256 creator_pubkey,string mime, string extension, bytes[] chunks) {
        return (
            m_chunks_count,
            m_cur_chunk_count,
            tvm.pubkey(),
            _mime,
            _extension,
            m_raw_data_chunks
        );
    }
}
