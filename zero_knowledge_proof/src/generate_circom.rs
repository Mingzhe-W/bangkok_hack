use plonky2_circom::generate_circom_verifier;

fn main() {
    // read verification_key.json
    let vk =
        serde_json::from_str(&std::fs::read_to_string("verification_key.json").unwrap()).unwrap();
    // generate Circom
    let circom_verifier = generate_circom_verifier(vk).unwrap();

    // write Circom
    std::fs::write("constants.circom", circom_verifier.constants).unwrap();
    std::fs::write("gates.circom", circom_verifier.gates).unwrap();
    println!("Circom verifier files generated successfully.");
}
