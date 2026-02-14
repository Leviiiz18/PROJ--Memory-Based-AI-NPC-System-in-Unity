using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class NPCWander : MonoBehaviour
{
    public float moveSpeed = 2f;
    public float changeDirectionTime = 3f;

    private Rigidbody2D rb;
    private Vector2 movement;
    private float timer;

    public bool canMove = true;   // IMPORTANT

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        ChooseNewDirection();
    }

    void Update()
    {
        if (!canMove) return;

        timer -= Time.deltaTime;

        if (timer <= 0f)
        {
            ChooseNewDirection();
        }
    }

    void FixedUpdate()
    {
        if (canMove)
            rb.linearVelocity = movement * moveSpeed;
        else
            rb.linearVelocity = Vector2.zero;
    }

    void ChooseNewDirection()
    {
        timer = changeDirectionTime;

        float x = Random.Range(-1f, 1f);
        float y = Random.Range(-1f, 1f);

        movement = new Vector2(x, y).normalized;
    }
}