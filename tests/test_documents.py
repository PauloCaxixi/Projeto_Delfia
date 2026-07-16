from pathlib import Path


def create_pdf():
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<<>>\n"
        b"endobj\n"
        b"trailer\n"
        b"<<>>\n"
        b"%%EOF"
    )


def test_upload_document(
    client,
    authentication,
):
    pdf_content = create_pdf()

    response = client.post(
        "/documents",
        auth=authentication,
        files={
            "file": (
                "teste.pdf",
                pdf_content,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_name"] == "teste.pdf"
    assert data["content_type"] == "application/pdf"
    assert data["size"] == len(pdf_content)
    assert "id" in data

    encrypted_files = list(Path("storage").glob("*.enc"))

    assert len(encrypted_files) == 1

    encrypted_content = encrypted_files[0].read_bytes()

    assert encrypted_content != pdf_content
    assert not encrypted_content.startswith(b"%PDF-")


def test_list_documents(
    client,
    authentication,
):
    client.post(
        "/documents",
        auth=authentication,
        files={
            "file": (
                "teste.pdf",
                create_pdf(),
                "application/pdf",
            )
        },
    )

    response = client.get(
        "/documents",
        auth=authentication,
    )

    assert response.status_code == 200

    assert len(response.json()) == 1


def test_download_document(
    client,
    authentication,
):
    upload = client.post(
        "/documents",
        auth=authentication,
        files={
            "file": (
                "teste.pdf",
                create_pdf(),
                "application/pdf",
            )
        },
    )

    document_id = upload.json()["id"]

    response = client.get(
        f"/documents/{document_id}/download",
        auth=authentication,
    )

    assert response.status_code == 200

    assert response.content.startswith(
        b"%PDF-"
    )


def test_should_reject_non_pdf(
    client,
    authentication,
):
    response = client.post(
        "/documents",
        auth=authentication,
        files={
            "file": (
                "arquivo.txt",
                b"teste",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400


def test_should_return_404(
    client,
    authentication,
):
    response = client.get(
        "/documents/nao-existe/download",
        auth=authentication,
    )

    assert response.status_code == 404