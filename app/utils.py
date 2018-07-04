import chilkat


def get_rsa_public_key_from_jwks(kty, e, n):
    json = chilkat.CkJsonObject()
    json.UpdateString("kty", kty)
    json.UpdateString("n", n)
    json.UpdateString("e", e)
    json.put_EmitCompact(False)

    jwkStr = json.emit()
    pubKey = chilkat.CkPublicKey()
    success = pubKey.LoadFromString(jwkStr)
    bPreferPkcs1 = False
    return pubKey.getPem(bPreferPkcs1)
