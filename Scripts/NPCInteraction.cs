using UnityEngine;

public class NPCInteraction : MonoBehaviour
{
    private bool playerNearby = false;
    private bool isTalking = false;

    private DialogueManager dialogueManager;
    private NPCWander wanderScript;

    private string npcName;

    void Start()
    {
        dialogueManager = FindObjectOfType<DialogueManager>();
        wanderScript = GetComponent<NPCWander>();

        // Automatically use GameObject name
        npcName = gameObject.name;
    }

    void Update()
    {
        if (playerNearby && !isTalking && Input.GetKeyDown(KeyCode.E))
        {
            isTalking = true;

            if (wanderScript != null)
                wanderScript.canMove = false;

            dialogueManager.StartDialogue(npcName, this);
        }
    }

    public void EndConversation()
    {
        isTalking = false;

        if (wanderScript != null)
            wanderScript.canMove = true;
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
            playerNearby = true;
    }

    void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            playerNearby = false;

            if (isTalking)
            {
                dialogueManager.EndDialogue();
                isTalking = false;

                if (wanderScript != null)
                    wanderScript.canMove = true;
            }
        }
    }
}