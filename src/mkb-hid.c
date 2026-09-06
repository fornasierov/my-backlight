#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define IOCTL_BASE 0xC0004806UL
#define FIRMWARE_REPORT_ID 0x0B
#define COLOR_REPORT_ID 0x05
#define HOST_MODE 0x00

static int parse_byte(const char *text, unsigned int *value) {
    char *end = NULL;
    unsigned long parsed;

    errno = 0;
    parsed = strtoul(text, &end, 10);
    if (errno != 0 || *text == '\0' || *end != '\0' || parsed > 255) {
        return -1;
    }

    *value = (unsigned int)parsed;
    return 0;
}

static int set_feature(int fd, unsigned int report_id, const unsigned char *payload,
                      size_t payload_length) {
    unsigned char buffer[32];
    size_t length = payload_length + 1;

    if (length > sizeof(buffer)) {
        fprintf(stderr, "HID report is too large\n");
        return -1;
    }

    buffer[0] = (unsigned char)report_id;
    memcpy(buffer + 1, payload, payload_length);

    if (ioctl(fd, IOCTL_BASE | (length << 16), buffer) < 0) {
        fprintf(stderr, "HID ioctl failed: %s\n", strerror(errno));
        return -1;
    }

    return 0;
}

int main(int argc, char **argv) {
    unsigned int red, green, blue, intensity;
    unsigned char host_payload[] = {HOST_MODE};
    unsigned char color_payload[9] = {1, 0, 0, 0, 0, 0, 0, 0, 0};
    int fd;
    int result = EXIT_FAILURE;

    if (argc != 6) {
        fprintf(stderr, "Usage: %s DEVICE RED GREEN BLUE INTENSITY\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (parse_byte(argv[2], &red) < 0 || parse_byte(argv[3], &green) < 0 ||
        parse_byte(argv[4], &blue) < 0 || parse_byte(argv[5], &intensity) < 0) {
        fprintf(stderr, "Color and intensity values must be integers from 0 to 255\n");
        return EXIT_FAILURE;
    }

    color_payload[5] = (unsigned char)red;
    color_payload[6] = (unsigned char)green;
    color_payload[7] = (unsigned char)blue;
    color_payload[8] = (unsigned char)intensity;

    fd = open(argv[1], O_RDWR | O_CLOEXEC);
    if (fd < 0) {
        fprintf(stderr, "Cannot open %s: %s\n", argv[1], strerror(errno));
        return EXIT_FAILURE;
    }

    if (set_feature(fd, FIRMWARE_REPORT_ID, host_payload, sizeof(host_payload)) == 0 &&
        set_feature(fd, COLOR_REPORT_ID, color_payload, sizeof(color_payload)) == 0) {
        result = EXIT_SUCCESS;
    }

    close(fd);
    return result;
}
