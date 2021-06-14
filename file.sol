pragma ton-solidity >= 0.35.0;
pragma AbiHeader time;
pragma AbiHeader expire;

contract tonFile {
    uint8 constant MAX_CLEANUP_MSGS = 30;
    mapping(uint => uint32) messages;
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
    uint128 static nonce;
    address public static m_root_address;
    uint128 m_chunks_count;
    uint128 m_cur_chunk_count;
    address allowance_dest;

    bytes[] public m_raw_data_chunks;

    constructor(uint8 chunks_count) public {
        require(tvm.pubkey() != 0, 101);
        require(chunks_count > 0, ERROR_CHUNKS_COUNT_MUST_BE_ABOVE_THAN_ZERO);
        tvm.accept();
        
        m_chunks_count = chunks_count;
        m_raw_data_chunks = new bytes[](m_chunks_count);
    }

    modifier onlyOwnerAndAccept {
        require(msg.pubkey() == tvm.pubkey(), 102);
        tvm.accept();
        _;
    }

    function writeData(uint128 index, bytes chunk) public onlyOwnerAndAccept{
        require(msg.pubkey() == tvm.pubkey(), ERROR_SENDER_IS_NOT_MY_OWNER);
        require(m_raw_data_chunks[index].length == uint(0), ERROR_CHUNK_ALREADY_EXISTS);
        require(index <= m_chunks_count, ERROR_INCORRECT_INDEX);
        require(m_cur_chunk_count <= m_chunks_count, ERROR_INCORRECT_CHUNKS_COUNT);
        tvm.accept();

        m_raw_data_chunks[index] = chunk;

        ++m_cur_chunk_count;
        gc();
    }

    function afterSignatureCheck(TvmSlice body, TvmCell message) private inline returns (TvmSlice) {
        body.decode(uint64);
        uint32 expireAt = body.decode(uint32);
        require(expireAt >= now, 101);
        uint hash = tvm.hash(message);
        require(!messages.exists(hash), 102);
        messages[hash] = expireAt;
        return body;
    }
    function getDetails() public view returns (uint128 chunks_count, uint128 cur_chunk_count, uint256 creator_pubkey, bytes[] chunks) {
        return (
            m_chunks_count,
            m_cur_chunk_count,
            tvm.pubkey(),
            m_raw_data_chunks
        );
    }
    function getData(uint128 index) public view returns (bytes data) {
        return (m_raw_data_chunks[index]);

    }

    function gc() private {
        optional(uint256, uint32) res = messages.min();
        uint8 counter = 0;
        while (res.hasValue() && counter < MAX_CLEANUP_MSGS) {
            (uint256 msgHash, uint32 expireAt) = res.get();
            if (expireAt < now) {
                delete messages[msgHash];
            }
            counter++;
            res = messages.next(msgHash);
        }
    }
}
